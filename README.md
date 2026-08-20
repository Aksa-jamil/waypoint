# Waypoint

Waypoint is a Django web application built around a hiking trail domain engine. The project was developed incrementally through Weeks 7-14, progressing from domain modeling to a Django web application with database relationships, validation, testing, and final handoff.

## Features

- Hiking trail domain model with different trail types
- Distance value object with unit conversion and validation
- Django Model-View-Template (MVT) architecture
- Trail catalog with open-trail filtering
- Park model related to trails through a ForeignKey
- Park-based trail filtering
- Django admin management for Parks and Trails
- Trail detail pages with 404 handling
- Automated domain and Django tests

## Requirements

- Python 3.12+
- Django 4.2
- pytest
- Git

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Aksa-jamil/waypoint.git
cd waypoint