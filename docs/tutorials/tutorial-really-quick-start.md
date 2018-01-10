---
layout: default
title: The Scientific Filesystem (Really) Quick Start
pdf: true
permalink: /tutorial-really-quick-start
toc: false
---

Same commands, but [more detail here](/scif/tutorial-quick-start).

## 1. Get containers with the same scientific filesystem

```
singularity pull --name scif-cli shub://vsoch/scif:scif
docker pull vanessa/scif
```

## 2. View the scientific filesystem entrypoint
```
docker run vanessa/scif
./scif-cli 
```

## 3. Discover Installed Apps
```
docker run vanessa/scif apps
./scif-cli apps
```

## 4. Commands
### Help
```
docker run vanessa/scif help hello-world-env
./scif-cli help hello-world-env
```
### Inspect
```
docker run vanessa/scif inspect hello-world-env
./scif-cli inspect hello-world-env
```
### Run

```
docker run vanessa/scif run hello-world-echo
./scif-cli run hello-world-echo
```

### Execute
```
docker run vanessa/scif exec hello-world-echo echo "Another hello!"
./scif-cli exec hello-world-echo echo "Another hello!"
```

### Execute command with environment variable $OMG
```
docker run vanessa/scif exec hello-world-env echo [e]OMG
./scif-cli exec hello-world-env echo [e]OMG
```

### Interactive shell
```
./scif-cli shell
docker run -it vanessa/scif shell
```

### Shell with application active
```
 ./scif-cli shell hello-world-env
docker run -it vanessa/scif shell hello-world-env
```

### Python interactive client
```
./scif-cli pyshell
docker run -it vanessa/scif pyshell
```
