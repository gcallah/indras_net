Write-Host "Windows Powershell Script for Indra Docker Container"
Write-Host "**Remove any still open indra-dev containers"
docker rm indra-dev -f
#If this doesn't run and/or crashed immediately AND you are using a VM 
#Use this in powershell (without the $):
#$docker-machine regenerate-certs <DOCKER MACHINE IMAGE NAME>
#The machine image name is probably "default"
#For security purposes this should not be run every time container.ps1 is used
Write-Host ""
Write-Host "**If docker is using a VM one must open virtualBox"
Write-Host "**Select your Docker Machine VirtualBox image (e.g.: default)"
Write-Host "**Open Settings -> Network -> Advanced -> Port Forward"
Write-Host "**Add: Django, TCP, 0.0.0.0, 8000, , 8000"
#If someone is not using the Pro/Enterprise editions of windows, they can only install
#a version of docker that is on VirtualBox. So this applies to most people.
Write-Host ""
Write-Host "**Now running docker to spin up the container"
Write-Host "**To start the Django server use 'runserver.sh'"
Write-Host "**Use '127.0.0.1:8000' to connect to site after"
Write-Host ""
$absolutePath = ('/'+(($pwd.Path[0] -join '').toLower() )+($pwd.Path.Substring($pwd.path.IndexOf(':')+1) -replace'\\','/'))
docker run -it -p 8000:8000 --mount type=bind,src="$absolutePath",dst="/home/IndrasNet" -w /home/IndrasNet --name indra-dev gcallah/indra-dev:latest bash
