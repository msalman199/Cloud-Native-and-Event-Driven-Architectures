# TODO: Use nginx:alpine as base image
FROM nginx:alpine

# TODO: Copy custom nginx configuration
# Replace default config at /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# TODO: Copy HTML file to nginx html directory
COPY index.html /usr/share/nginx/html/

# TODO: Expose port 80
EXPOSE 80

# Note: nginx image has default CMD, no need to specify
