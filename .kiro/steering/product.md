---
inclusion: auto
---

# DataForge Product Overview

DataForge is a high-efficiency, flexible, and highly configurable test data generation tool designed for software testing teams. It specializes in generating high-quality, realistic, and diverse test data with deep optimization for Chinese localization.

## Core Purpose

Generate production-grade test data for software testing, with particular focus on:
- Chinese-specific data types (ID cards, bank cards, phone numbers, social credit codes)
- Data relationship consistency across fields
- High-performance batch generation
- Multiple output formats (JSON, CSV, XML, SQL, YAML)

## Key Features

- **Chinese Localization**: Native support for Chinese ID cards, bank cards, phone numbers, unified social credit codes, and administrative regions
- **Data Relationships**: Logical associations between fields to ensure data consistency
- **Extensibility**: Plugin architecture for custom generators
- **Multi-format Output**: JSON, CSV, XML, SQL, YAML support
- **Dual Interface**: CLI tool and Python API
- **Web Console**: Vue 3-based web interface for visual data generation

## Target Users

- Software testing engineers
- QA teams
- Development teams needing mock data
- Data analysts requiring sample datasets

## Project Components

1. **Core Library** (`dataforge/`): Python-based data generation engine
2. **CLI Tool**: Command-line interface for quick data generation
3. **Web Console** (`web-console/`): Vue 3 + TypeScript frontend
4. **API Service**: FastAPI-based REST API for remote generation
