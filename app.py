from app import app, routes
# from waitress import serve

# Initialize Server
if __name__ == '__main__':
    
    # serve using waitress
    # serve(app, host="0.0.0.0", port=5000)

    # serve using flask build-in development server 
    app.run(debug=False, host='0.0.0.0', port=5000)