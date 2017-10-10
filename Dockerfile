FROM nginx
# Copy the static website and all js files and images
COPY website /usr/share/nginx/html
# Add priviliges for images, otherwise nginx has no right to serve them and they would be missing
RUN chmod -R 0777 /usr/share/nginx/html/img