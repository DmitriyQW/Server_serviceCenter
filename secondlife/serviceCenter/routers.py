from rest_framework import  routers
from .views import UsersViewSet, WorkerViewSet, ApplicationViewSet, State_applicSet

routerUsers = routers.SimpleRouter()
routerUsers.register(r'users',UsersViewSet)
# 127.0.0.1:8000/api/v1/users/

routerWorker = routers.SimpleRouter()
routerWorker.register(r'workers',WorkerViewSet)
# 127.0.0.1:8000/api/v1/works/

routerApplication = routers.SimpleRouter()
routerApplication.register(r'application',ApplicationViewSet)
# http://127.0.0.1:8000/api/v1/application/

routerState_applic = routers.SimpleRouter()
routerState_applic.register(r'state_applic',State_applicSet)
# http://127.0.0.1:8000/api/v1/state_applic/

urlsapi = routerUsers.urls + routerWorker.urls + routerApplication.urls + routerState_applic.urls