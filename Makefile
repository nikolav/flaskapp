
# Variables
SERVICE_NGINX := nginx

# Colors
GREEN  := \033[0;32m
YELLOW := \033[1;33m
RED    := \033[0;31m
RESET  := \033[0m

# ============================
#  System
# ============================

.PHONY: restart-nginx
restart-nginx:
	@echo "$(YELLOW)[*] Restarting nginx...$(RESET)"
	@systemctl restart $(SERVICE_NGINX)
	@systemctl status $(SERVICE_NGINX) --no-pager | head -n 10
	@echo "$(GREEN)[✓] Nginx restarted.$(RESET)"

# ============================
#  Deployment
# ============================

# Setup env
.PHONY: deploy-env
deploy-env:
	@echo "$(YELLOW)[*] Setting up environment...$(RESET)"
	@. ./deploy-env.sh
	@echo "$(GREEN)[✓] Environment ready.$(RESET)"

# Full clean rebuild
.PHONY: deploy-clean
deploy-clean:
	@echo "$(YELLOW)[*] Cleaning Docker resources and redeploying...$(RESET)"
	@docker compose down --remove-orphans
	@docker system prune -af
	@$(MAKE) deploy
	@echo "$(GREEN)[✓] Fresh deployment completed.$(RESET)"s

# Deploy
.PHONY: deploy
deploy:
	@echo "$(YELLOW)[*] Deploying app...$(RESET)"
	@. ./deploy.sh
	@echo "$(GREEN)[✓] Deployment finished.$(RESET)"

# ============================
#  Docker Maintenance
# ============================

.PHONY: docker-clean
docker-clean:
	@echo "$(YELLOW)[*] Cleaning all unused Docker data...$(RESET)"
	@docker system prune -a -f
	@echo "$(GREEN)[✓] Docker cleaned.$(RESET)"

.PHONY: docker-reset
docker-reset:
	@echo "$(YELLOW)[*] Stopping and removing ALL containers, images, volumes, and networks...$(RESET)"
	@docker stop $$(docker ps -aq) 2>/dev/null || true
	@docker rm -f $$(docker ps -aq) 2>/dev/null || true
	@docker rmi -f $$(docker images -q) 2>/dev/null || true
	@docker volume rm -f $$(docker volume ls -q) 2>/dev/null || true
	@docker network prune -f
	@echo "$(GREEN)[✓] Docker fully reset.$(RESET)"

