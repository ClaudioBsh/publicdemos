# Stop App
docker stop myniceguidemo
docker rm myniceguidemo

# Run App in Background
docker run -d -p 8080:8080 --name myniceguidemo myniceguidemo
echo "MyNiceGuiDemo is running on (Port 8080):"
hostname -I
echo ""
sleep 5
docker logs myniceguidemo
