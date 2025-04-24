FROM node
COPY . .
EXPOSE 3001
WORKDIR Interface
RUN chmod +x mount_smb.sh
RUN npm install
CMD ["npm","start"]