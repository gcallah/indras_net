Write-Host "Windows Powershell Script for Indra Docker Container"
Write-Host "**Remove any still open indra containers"
docker rm indra -f
Write-Host "**Now running docker to spin up the container."
$absolutePath = ('/'+(($pwd.Path[0] -join '').toLower() )+($pwd.Path.Substring($pwd.path.IndexOf(':')+1) -replace'\\','/'))
docker run -it -p 8000:8000 --mount type=bind,src="$absolutePath",dst="/home/IndrasNet" -w /home/IndrasNet --name indra gcallah/indra:v7 bash