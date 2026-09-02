#!/usr/bin/env python3
"""Detect shared audio between two MP3 recordings.

The recordings are decoded with ffmpeg, aligned using normalized
cross-correlation, and inspected in short frames around the best alignment.
The output is intended to be readable in a terminal and contains timestamps
in both source recordings.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np


DEFAULT_SAMPLE_RATE = 4000
DEFAULT_FRAME_SECONDS = 0.5
DEFAULT_HOP_SECONDS = 0.1
DEFAULT_THRESHOLD = 0.55


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find segments shared by two MP3 recordings."
    )
    parser.add_argument("recording1", type=Path, help="First MP3 recording.")
    parser.add_argument("recording2", type=Path, help="Second MP3 recording.")
    parser.add_argument(
        "--mode",
        choices=("general", "contained"),
        default="general",
        help="Detection strategy (default: general).",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help=f"Minimum frame correlation (default: {DEFAULT_THRESHOLD}).",
    )
    parser.add_argument(
        "--frame-seconds",
        type=float,
        default=DEFAULT_FRAME_SECONDS,
        help=f"Correlation frame length in seconds (default: {DEFAULT_FRAME_SECONDS}).",
    )
    parser.add_argument(
        "--hop-seconds",
        type=float,
        default=DEFAULT_HOP_SECONDS,
        help=f"Distance between frames in seconds (default: {DEFAULT_HOP_SECONDS}).",
    )
    return parser.parse_args()


def read_audio(path, sample_rate=DEFAULT_SAMPLE_RATE):
    """Decode an audio file to mono float32 samples using ffmpeg."""
    command = [
        "ffmpeg",
        "-v",
        "error",
        "-i",
        str(path),
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "-f",
        "f32le",
        "-",
    ]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE)
    except FileNotFoundError as error:
        raise RuntimeError("ffmpeg is required but was not found on PATH.") from error
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f"Could not decode {path}.") from error

    samples = np.frombuffer(result.stdout, dtype=np.float32).copy()
    if samples.size == 0:
        raise RuntimeError(f"{path} contains no decodable audio.")
    return samples


def best_alignment(first, second):
    """Return the lag at which ``second`` best matches ``first``."""
    first = first - np.mean(first)
    second = second - np.mean(second)
    size = first.size + second.size - 1
    fft_size = 1 << (size - 1).bit_length()
    correlation = np.fft.irfft(
        np.fft.rfft(first, fft_size) * np.conj(np.fft.rfft(second, fft_size)),
        fft_size,
    )
    correlation = np.concatenate((correlation[-(second.size - 1) :], correlation[: first.size]))
    lag = int(np.argmax(correlation)) - (second.size - 1)
    return lag


def best_contained_alignment(longer, shorter):
    """Return the offset and correlation of the shorter signal in the longer one."""
    if shorter.size > longer.size:
        raise ValueError("The first signal must be at least as long as the second.")

    longer = longer - np.mean(longer)
    shorter = shorter - np.mean(shorter)
    short_norm = np.linalg.norm(shorter)
    if short_norm == 0:
        return 0, 0.0

    size = longer.size + shorter.size - 1
    fft_size = 1 << (size - 1).bit_length()
    full_correlation = np.fft.irfft(
        np.fft.rfft(longer, fft_size) * np.conj(np.fft.rfft(shorter, fft_size)),
        fft_size,
    )
    full_correlation = np.concatenate(
        (full_correlation[-(shorter.size - 1) :], full_correlation[: longer.size])
    )
    correlation = full_correlation[shorter.size - 1 : longer.size]
    squared = longer * longer
    cumulative = np.concatenate(([0.0], np.cumsum(squared)))
    window_norm = np.sqrt(cumulative[shorter.size :] - cumulative[:-shorter.size])
    denominator = window_norm * short_norm
    normalized = np.divide(
        correlation,
        denominator,
        out=np.zeros_like(correlation),
        where=denominator != 0,
    )
    offset = int(np.argmax(normalized))
    return offset, float(normalized[offset])


def frame_correlation(first, second):
    first = first - np.mean(first)
    second = second - np.mean(second)
    denominator = np.linalg.norm(first) * np.linalg.norm(second)
    if denominator == 0:
        return 0.0
    return float(np.dot(first, second) / denominator)


def find_segments(first, second, lag, sample_rate, frame_seconds, hop_seconds, threshold):
    """Find contiguous high-correlation frames and return their sample ranges."""
    frame_size = max(1, round(frame_seconds * sample_rate))
    hop_size = max(1, round(hop_seconds * sample_rate))
    candidates = []

    # ``lag`` is the start of second recording measured in first-recording
    # samples: first[lag + i] corresponds to second[i].
    second_start = max(0, -lag)
    first_start = max(0, lag)
    shared_length = min(first.size - first_start, second.size - second_start)
    if shared_length < frame_size:
        return []

    for offset in range(0, shared_length - frame_size + 1, hop_size):
        first_frame = first[first_start + offset : first_start + offset + frame_size]
        second_frame = second[second_start + offset : second_start + offset + frame_size]
        if frame_correlation(first_frame, second_frame) >= threshold:
            candidates.append(offset)

    segments = []
    if not candidates:
        return segments
    start = previous = candidates[0]
    max_gap = hop_size * 1.5
    for offset in candidates[1:]:
        if offset - previous > max_gap:
            segments.append((start, previous + frame_size))
            start = offset
        previous = offset
    segments.append((start, previous + frame_size))

    return [
        (
            first_start + start,
            first_start + end,
            second_start + start,
            second_start + end,
        )
        for start, end in segments
    ]


def format_time(sample, sample_rate):
    seconds = sample / sample_rate
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:05.2f}"


def main():
    args = parse_args()
    if not 0 <= args.threshold <= 1:
        raise ValueError("--threshold must be between 0 and 1.")
    if args.frame_seconds <= 0 or args.hop_seconds <= 0:
        raise ValueError("Frame and hop lengths must be positive.")

    first = read_audio(args.recording1)
    second = read_audio(args.recording2)
    sample_rate = DEFAULT_SAMPLE_RATE
    if args.mode == "contained":
        if first.size >= second.size:
            offset, score = best_contained_alignment(first, second)
            segments = (
                [(offset, offset + second.size, 0, second.size)]
                if score >= args.threshold
                else []
            )
        else:
            offset, score = best_contained_alignment(second, first)
            segments = (
                [(0, first.size, offset, offset + first.size)]
                if score >= args.threshold
                else []
            )
    else:
        lag = best_alignment(first, second)
        segments = find_segments(
            first,
            second,
            lag,
            sample_rate,
            args.frame_seconds,
            args.hop_seconds,
            args.threshold,
        )

    print(f"Overlap detected: {'yes' if segments else 'no'}")
    for index, (first_start, first_end, second_start, second_end) in enumerate(segments, 1):
        print(f"Segment {index}:")
        print(
            f"  {args.recording1}: {format_time(first_start, sample_rate)} - "
            f"{format_time(first_end, sample_rate)}"
        )
        print(
            f"  {args.recording2}: {format_time(second_start, sample_rate)} - "
            f"{format_time(second_end, sample_rate)}"
        )


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(2)
