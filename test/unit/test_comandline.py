from flexmock import flexmock

from meteoservice.commandline import App


# noinspection PyMethodMayBeStatic
class TestCommandLine:

    def test_ask_for_temperature_data(self):
        wsconsumer = flexmock()
        app = App(wsconsumer)

        (wsconsumer
            .should_receive('register_handler')
            .with_args(str, object)
            .at_least()
            .once()
            .ordered())
        (wsconsumer
            .should_receive('temperature')
            .with_args()
            .once()
            .ordered())

        app.main()

    def test_handler_outputs_received_temperature(self, capsys):
        app = App(wsconsumer=None)
        event = flexmock(data={'temperature': 18})

        app.data_received_handler(event)

        out, err = capsys.readouterr()
        assert '18 ℃' in out
