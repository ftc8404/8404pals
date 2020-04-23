FROM openjdk:8-jdk-alpine
LABEL maintainer="FTC 8404 Quixilver <niemiryan@gmail.com>"
ENV REFRESHED_AT 2020-04-22
EXPOSE 8080
RUN set -ex \
  && apk update \
  && apk upgrade
RUN mkdir /auth-api
COPY /build/libs/*.jar /auth-api/users.jar
WORKDIR /auth-api
CMD ["java", "-jar", "-Djava.security.egd=file:/dev/./urandom", "-Dspring.profiles.active=docker", "users.jar"]
