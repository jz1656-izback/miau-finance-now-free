FROM node:20-alpine AS builder

WORKDIR /build

COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps && npm cache clean --force

COPY . .
RUN npm run build && \
    find /build/dist -name "*.map" -delete

FROM node:20-alpine AS development

WORKDIR /build

COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps --include=dev && npm cache clean --force

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

FROM nginx:alpine AS production

RUN rm -rf /etc/nginx/conf.d/default.conf && \
    adduser -D -H -u 1000 -s /bin/nologin nginxuser

COPY nginx-pwa.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /build/dist /usr/share/nginx/html
COPY --chown=nginxuser:nginxuser --from=builder /build/dist /usr/share/nginx/html

EXPOSE 80

USER nginxuser

CMD ["nginx", "-g", "daemon off;"]
