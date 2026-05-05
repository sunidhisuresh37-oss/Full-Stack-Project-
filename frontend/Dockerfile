# Use official Nginx image as the base image
FROM nginx:alpine

# Copy the static HTML, CSS, and JS files to the default Nginx public folder
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/

# Expose port 80 to the outside world
EXPOSE 80

# Nginx starts automatically
