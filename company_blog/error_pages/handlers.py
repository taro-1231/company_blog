from flask import render_template,Blueprint

error_pages=Blueprint('error_pages',__name__)

# error_pagesでは1つのブループリント内だけになる。アプリケーション全体にするためにはapp_errorhandler
@error_pages.app_errorhandler(403)
def error_404(error):
    return render_template('error_pages/403.html'),403

@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html'),404
