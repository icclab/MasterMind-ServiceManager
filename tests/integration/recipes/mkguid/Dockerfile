FROM mhart/alpine-node:4.4

RUN apk --update add curl
ADD package.json /package.json
# WORKDIR /root
RUN npm i
ADD app.js /app.js

EXPOSE 9000

# HEALTHCHECK CMD curl --fail http://localhost:9000/guid/ || exit 1

CMD ["npm", "start"]
