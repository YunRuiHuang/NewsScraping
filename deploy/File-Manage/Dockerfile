FROM node

EXPOSE 3000

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

RUN chmod +x mount_smb.sh

RUN mkdir -p /app/public

CMD ["npm","start"]