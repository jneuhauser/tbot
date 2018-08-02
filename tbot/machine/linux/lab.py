import abc
import pathlib
import paramiko
from tbot.machine import linux
from tbot.machine.linux import auth


class LabHost(linux.LinuxMachine):
    @property
    @abc.abstractmethod
    def hostname(self) -> str:
        """Return the hostname of this lab."""
        pass

    @property
    def authenticator(self) -> auth.Authenticator:
        """Return an authenticator that allows loggin in on the labhost."""
        return auth.PrivateKeyAuthenticator(
            pathlib.Path.home() / ".ssh" / "id_rsa",
        )

    @property
    def port(self) -> int:
        """Return the port the SSH server is listening on."""
        return 22

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __init__(self) -> None:
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()

        password = None
        key_file = None

        authenticator = self.authenticator
        if isinstance(authenticator, auth.PasswordAuthenticator):
            password = authenticator.password
        if isinstance(authenticator, auth.PrivateKeyAuthenticator):
            key_file = str(authenticator.key)

        self.client.connect(
            self.hostname,
            port=self.port,
            password=password,
            key_filename=key_file,
        )

    def destroy(self) -> None:
        self.client.close()

    def _obtain_channel(self) -> paramiko.Channel:
        return self.client.get_transport().open_session()
