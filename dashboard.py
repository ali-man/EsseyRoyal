from admin_tools.dashboard import modules, Dashboard


class MyModule(modules.DashboardModule):

    def is_empty(self):
        pass

    def __init__(self, **kwargs):
        super(MyModule, self).__init__(**kwargs)


class CustomIndexDashboard(Dashboard):

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        self.children.append(
            modules.Group(
                title='Main',
                display='tabs',
                children=[
                    modules.ModelList(
                        title='Profiles',
                        models=(
                            'appprofile.models.Client',
                            'appprofile.models.Manager',
                            'appprofile.models.Writer',
                        )
                    ),
                    modules.ModelList(
                        title='Orders',
                        models=(
                            'apporders.models.FormatOrder',
                            'apporders.models.Earning',
                            'apporders.models.FormatOrder',
                            'apporders.models.Order',
                        )
                    ),
                    modules.ModelList(
                        title='Works',
                        models=(
                            'appwork.models.TypeWorks',
                        ),
                    ),
                ]
            )
        )

        self.children.append(
            modules.ModelList(
                title='Static Page',
                models=(
                    'django.contrib.flatpages.*',
                    'django.contrib.sites.*',
                ),
            )
        )

        self.children.append(
            modules.ModelList(
                title='Users',
                models=(
                    'django.contrib.auth.*',
                    'accounts.models.Profile',
                )
            )
        )

        self.children.append(
            modules.LinkList(
                title='Links',
                children=[
                    {
                        'title': 'Title link',
                        'url': '/dashboard/customer',
                        'external': False,
                        'attrs': {'target': '_blank'},
                    },
                ]
            )
        )