from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_hosts_file(File):
    hosts = File('/etc/hosts')

    assert hosts.user == 'root'
    assert hosts.group == 'root'

def test_celerybeat_running_and_enabled(Service):
    celerybeat = Service("celerybeat")
    assert celerybeat.is_running
    assert celerybeat.is_enabled

def test_celeryd_running_and_enabled(Service):
    celery = Service("celery")
    assert celery.is_running
    assert celery.is_enabled
