FROM node:22-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install pnpm and dependencies
RUN npm install -g pnpm
RUN pnpm install

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Default command for development
CMD ["pnpm", "run", "dev", "--host"]
