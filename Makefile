
# ============================
#  Basic Server Makefile
# ============================

# Variables
SERVICE_NGINX := nginx
SERVICE_API := api

# ============================
#  System Maintenance
# ============================

.PHONY: restart-nginx
restart-nginx:
	@sudo systemctl restart $(SERVICE_NGINX)
	@sudo systemctl status $(SERVICE_NGINX) --no-pager

# ============================
#  Deployment
# ============================

.PHONY: deploy-env
deploy-env:
	@echo "[*] Setting up environment..."
	@. ./deploy-env.sh

.PHONY: deploy
deploy:
	@echo "[*] Deploying app..."
	@. ./deploy.sh

# Full clean rebuild
.PHONY: deploy-clean
deploy-clean:
	@echo "[*] Cleaning Docker resources and redeploying..."
	@docker compose down --remove-orphans
	@docker system prune -af
	@make deploy
	@echo "[✓] Fresh deployment completed."

# ============================
#  Docker Maintenance
# ============================

.PHONY: docker-clean
docker-clean:
	@echo "[*] Cleaning all unused Docker data..."
	@docker system prune -a -f
	@echo "[✓] Docker cleaned."

.PHONY: docker-reset
docker-reset:
	@echo "[*] Stopping and removing all containers, images, and volumes..."
	@docker stop $$(docker ps -aq) 2>/dev/null || true
	@docker rm -f $$(docker ps -aq) 2>/dev/null || true
	@docker rmi -f $$(docker images -q) 2>/dev/null || true
	@docker volume rm -f $$(docker volume ls -q) 2>/dev/null || true
	@docker network prune -f
	@echo "[✓] Docker fully reset."

# ============================
#  Logs and Cleanup
# ============================

