FROM node:20-alpine as development

WORKDIR /srv/app

# install deps
COPY package.json package-lock.json* ./
RUN npm install

# copy source
COPY . .

EXPOSE 5173

# run Vite dev server
CMD ["npm", "run", "dev", "--", "--host"]