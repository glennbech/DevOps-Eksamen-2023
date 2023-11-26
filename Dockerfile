# Stage 1: Build Stage
FROM maven:3.6-jdk-11 AS Docker_Task

WORKDIR /app
# Copy only the necessary files for the build to leverage Docker cache
COPY pom.xml .
COPY src ./src

RUN mvn clean package

# Stage 2: Runtime Stage
FROM adoptopenjdk/openjdk11:jre-11.0.11_9-alpine
WORKDIR /app

# Copy the built JAR file from the builder stage
COPY --from=Docker_Task /app/target/*.jar app.jar
EXPOSE 8080

# Define the command to run the application
ENTRYPOINT ["java", "-jar", "app.jar"]