# Windows Powershell Script for Indra Docker Container
#Tell docker that we're using powershell
docker-machine env --shell=powershell | Invoke-Expression
#remove any still open indra containers
docker rm indra -f
#open container
docker run -it -p 8000:8000 -v ${PWD}:/home/IndrasNet indra bash
