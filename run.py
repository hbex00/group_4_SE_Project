from app.__init__ import create_app
app = create_app(URI='sqlite:///site.db')

if __name__ == '__main__':
    app.run(debug=True)