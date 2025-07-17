# VersaAI Docker Cleanup Script
Write-Host "=== VersaAI Docker Cleanup Script ===" -ForegroundColor Cyan
Write-Host "Cleaning up Docker environment..." -ForegroundColor Yellow

# Stop and remove all containers
Write-Host "Stopping and removing containers..." -ForegroundColor Yellow
docker stop $(docker ps -aq) 2>$null
docker rm -f $(docker ps -aq) 2>$null

# Remove all images
Write-Host "Removing images..." -ForegroundColor Yellow
docker rmi -f $(docker images -aq) 2>$null

# Remove all volumes
Write-Host "Removing volumes..." -ForegroundColor Yellow
docker volume rm -f $(docker volume ls -q) 2>$null

# Remove custom networks
Write-Host "Removing networks..." -ForegroundColor Yellow
docker network rm $(docker network ls --filter "type=custom" -q) 2>$null

# System cleanup
Write-Host "Running system cleanup..." -ForegroundColor Yellow
docker system prune -af --volumes 2>$null
docker builder prune -af 2>$null

# Clean local directories
Write-Host "Cleaning local directories..." -ForegroundColor Yellow
if (Test-Path "uploads") { Remove-Item -Path "uploads\*" -Recurse -Force -ErrorAction SilentlyContinue }
if (Test-Path "logs") { Remove-Item -Path "logs\*" -Recurse -Force -ErrorAction SilentlyContinue }

Write-Host "✅ Cleanup completed!" -ForegroundColor Green
Write-Host "Ready for fresh installation." -ForegroundColor Green