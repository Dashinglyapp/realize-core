from core.plugins.base import BasePlugin
from core.plugins.proxies import MetricProxy
from core.plugins.permissions import AuthorizationPermission
from models import MoodModel, DataModel, GithubCommits
from forms import SurveyForm, MoodForm
from tasks import ScrapeTask
from views import GetStuffView
from datetime import datetime
import manifest

class TestPlugin(BasePlugin):
    name = manifest.NAME
    description = manifest.DESCRIPTION
    models = [MoodModel, DataModel, GithubCommits]
    forms = [SurveyForm, MoodForm]
    tasks = [ScrapeTask]
    views = [GetStuffView]
    permissions = [AuthorizationPermission(name="github")]
    hashkey = manifest.HASHKEY

    def setup(self):
        moods = self.manager.query_time_filter(manifest.plugin_proxy, MetricProxy(name="mood"))
        if len(moods) == 0:
            mood = MoodModel(data=1, date=datetime.utcnow())
            self.manager.add(mood)
        data = self.manager.query_blob_filter(manifest.plugin_proxy, MetricProxy(name="data"))
        if len(data) == 0:
            data = DataModel(date=datetime.utcnow(), text="This is some text.", number=1)
            self.manager.add(data)

    def destroy(self):
        pass

    def save_forms(self, metric, **kwargs):
        if SurveyForm.metric_proxy.name == metric.name:
            form = SurveyForm(**kwargs)
            if form.validate():
                data = DataModel(date=datetime.utcnow(), text=form.text.data, number=form.number.data)
                self.manager.add(data)
        elif MoodForm.metric_proxy.name == metric.name:
            form = MoodForm(**kwargs)
            if form.validate():
                data = MoodModel(date=datetime.utcnow(), data=form.number.data)
                self.manager.add(data)