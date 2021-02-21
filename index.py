# import WeiXinCore.WeiXin
import sys
from imp import reload

reload(sys)
from FlaskApp import app

app.run(debug=True, port=5000)
