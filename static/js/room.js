
class InputText extends React.Component {
    render() {
        return (
        <div className="field is-grouped">
            <p className="control is-expanded">
                <input className="input" type="text" id="message_text" placeholder="Your message" />
            </p>
            <p className="control">
                <button className="button is-info" onClick={this.props.send_message}>
                    Send
                </button>
            </p>
        </div>
        );
    }
}

class Message extends React.Component {
    render() {
        return (
            <div className="is-clearfix is-fullwidth content">
                <p className={'notification is-info ' + (this.props.received ? 'is-pulled-left' : 'is-pulled-right')}>
                    {this.props.message.body}
                </p>
            </div>
        );
    }
}

class Inbox extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            message_list: [],
            new_message: null
        };
        this.send_message = this.send_message.bind(this);
    }

    send_message () {
        const new_message = {
            'timestamp': new Date(),
            "author": null,
            "body" : document.getElementById("message_text").value,
            "id": new Date()
        };
        this.setState(function(prevState) {
            return {
                message_list:  [...prevState.message_list, new_message]
            };
        });
    }

    scrollToBottom = () => {
        const node = ReactDOM.findDOMNode(this.message_list_end);
        node.scrollIntoView({ behavior: "smooth" });
    }

    componentDidMount () {
        this.scrollToBottom();
    }

    componentDidUpdate () {
        this.scrollToBottom();
    }

    render() {
        const current_channel = this.props.channel;
        const message_list = this.state.message_list;
        const messages =  message_list.map((message) =>
            <Message key={message.id} message={message} received={message.author !== null} />
        );
        const sticky_style = {
            left: '0',
            right: '0',
            bottom: '0',
            height: '70px',
            width: '100%',
            z_index: '254',
            position: 'fixed',
        };
        return (
            <div className="container is-overlay">
                {messages}
                <div ref={(el) => { this.message_list_end = el; }} />
                <div className="container notification is-primary" style={sticky_style}>
                    <InputText send_message={this.send_message} />
                </div>
            </div>
        )
    };
}

ReactDOM.render(
    <Inbox channel="test" />,
    document.getElementById('inbox')
);

ReactDOM.render(
    <div className="field has-addons">
        <p className="control">
            <input className="input" type="text" placeholder="Channel" />
        </p>
        <p className="control">
            <button className="button is-info">
                Join
            </button>
        </p>
    </div>,
    document.getElementById('channel_selector')
);
