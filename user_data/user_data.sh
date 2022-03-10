#!/bin/bash
sudo yum update -y
sudo docker pull sebranchett/gpaw:one_processor_21.1.0
sudo docker run --rm sebranchett/gpaw:one_processor_21.1.0 gpaw test
