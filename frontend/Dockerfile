# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:20 AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /app

RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=pnpm-lock.yaml,target=pnpm-lock.yaml \
    --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --prod --frozen-lockfile

USER node

COPY . .

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM base as dev
CMD ["pnpm", "dev"]

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1 as prod
COPY --from=build /app/dist/ /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
