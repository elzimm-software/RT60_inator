# SPIDAM: Scientific Python Interactive Data Acoustic Modeling

## Overview

The **SPIDAM** (Scientific Python Interactive Data Acoustic Modeling) project aims to develop an interactive platform for analyzing and modeling reverberation time (RT60) in enclosed spaces. The platform provides tools for importing, cleaning, visualizing, and modeling data related to reverberation, specifically targeting the problem of voice intelligibility in environments with high reverberation times. 

The goal is to improve voice intelligibility by measuring and analyzing reverberation time and providing insights into how different frequencies contribute to reverb in a space.

## Background

Reverberation (reverb) refers to the persistence of sound after the source has stopped, caused by reflections within an enclosed space. The time it takes for sound to decay by 60 dB is called RT60, which is an important metric for determining how sound behaves in a room. Long reverberation times can severely impair speech intelligibility, making communication difficult.

The objective of this project is to:
- Measure and analyze reverberation time (RT60) across different frequencies.
- Identify problematic frequency ranges with high reverb times.
- Provide recommendations for reducing reverberation in order to improve voice intelligibility.

## Functional Requirements

The SPIDAM platform will have the following core functionalities:

- **GUI Features**:
  - Load audio files (supports WAV, MP3, and AAC).
  - Automatically convert non-WAV files to WAV format if needed.
  - Handle metadata removal and multi-channel conversion.
  - Display various plots (waveform, RT60 plots for low, mid, and high frequencies).
  - Output text reports with RT60 time, frequency of greatest amplitude, and suggestions for reducing RT60 to 0.5 seconds.

- **Data Analysis**:
  - Generate RT60 values for low, mid, and high-frequency ranges.
  - Create visualizations like histograms, scatter plots, and box plots for analysis.
  - Summarize key metrics (e.g., RT60, frequency of greatest amplitude).

## Design

The project follows the **Model-View-Controller (MVC)** design pattern:

- **Model**: Contains data classes for handling audio samples and RT60 values.
- **View**: The graphical interface for users to interact with the data.
- **Controller**: Manages the flow of data between the model and view, and controls user interactions.

## Installation

To get started with the SPIDAM project, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/yourusername/SPIDAM.git
cd SPIDAM
pip install -r requirements.txt
