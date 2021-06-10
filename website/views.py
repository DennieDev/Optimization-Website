from flask import Blueprint, render_template, request, flash
from analyze import analyze_url, get_tps_color

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@views.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        url = request.form.get('timings')

        if len(url) < 4:
            flash('Please specify a valid URL', category='error')
        elif url.startswith("https://www.spigotmc.org/go/timings?url=") or url.startswith("https://timings.spigotmc.org"
                                                                                          "/?url="):
            flash('Spigot timings have limited information. Switch to Purpur for better timings analysis. All your '
                  'plugins will be compatible, and if you don\'t like it, you can easily switch back. ',
                  category='error')
        elif "?id=" not in url:
            flash('Please specify a valid URL', category='error')
        else:
            if url.startswith("https://timin") and "/d=" in url:
                url.replace("/d=", "/?id=")
            elif "#" in url:
                url = url.split("#")[0]

            return_list = analyze_url(url)
            tps_list = get_tps_color()

            return render_template("report.html", return_list=return_list, tps_list=tps_list)

    return render_template("home.html")
