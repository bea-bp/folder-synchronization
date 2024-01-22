# Folder Synchronization

## Description
Folder Synchronization is a Python script designed to synchronize files and folders between a source directory and a replica directory. The script continuously monitors the source directory and replicates its contents to the replica directory, ensuring both directories are kept in sync. It handles the creation, deletion, and updating of files and folders, and logs all actions performed during synchronization.

## Features
- **Directory Synchronization**: Synchronizes all files and folders from a source directory to a replica directory.
- **Continuous Monitoring**: Runs in a loop, checking for changes at specified intervals.
- **Logging**: Logs all synchronization activities to a specified log file.
- **File Content Verification**: Uses MD5 checksums to verify file content and ensure accurate replication.

## Requirements
- Python 3.x

## Installation
Clone the repository or download the script to your local machine.

## Usage
To use the Folder Synchronization, run the script from the command line with the following arguments:

```bash
python folderSynchronization.py <source_directory> <replica_directory> <interval_in_seconds> <log_file_path>
