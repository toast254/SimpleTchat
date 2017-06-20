
class InputText extends React.Component {

    constructor(props) {
        super(props);
        this.key_enter = this.key_enter.bind(this);
    }

    key_enter (event) {
         if(event.charCode == 13){
            this.props.send_message();
         }
    }

    render() {
        const input_message = this.props.input_message;
        return (
        <div className="field is-grouped">
            <p className="control is-expanded">
                <input className="input" type="text" id="message_text" placeholder="Your message" onKeyPress={this.key_enter} value={input_message} onChange={this.props.change_input_message} />
            </p>
            <p className="control">
                <button className="button is-info" onClick={this.props.send_message} disabled={!input_message}>
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

    scrollToBottom = () => {
        const node = ReactDOM.findDOMNode(this.message_list_end);
        // node.scrollIntoView({ behavior: "smooth" }); // too slow ...
        node.scrollIntoView();
    }

    componentDidMount () {
        this.scrollToBottom();
    }

    componentDidUpdate () {
        this.scrollToBottom();
    }

    render() {
        const message_list = this.props.message_list;
        const messages =  message_list.map((message) =>
            <Message key={message.id} message={message} received={message.author !== this.props.current_user} />
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
                    <InputText send_message={this.props.send_message} input_message={this.props.input_message} change_input_message={this.props.change_input_message} />
                </div>
            </div>
        )
    };
}

class ChannelSelector extends React.Component {

    constructor(props) {
        super(props);
        this.key_enter = this.key_enter.bind(this);
    }

    key_enter (event){
         if(event.charCode == 13){
            this.props.choose_channel();
         }
    }

    render () {
        const channel_choice = this.props.channel_choice;
        return (
            <div className="field has-addons">
                <p className="control">
                    <input className="input" type="text" placeholder="Channel" id="channel_text" value={channel_choice} onChange={this.props.change_channel_choice} onKeyPress={this.key_enter} />
                </p>
                <p className="control">
                    <button className="button is-info" onClick={this.props.choose_channel} disabled={!channel_choice}>
                        Join
                    </button>
                </p>
            </div>
        )
    }
}

class Room extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            current_channel: null,
            current_user: null,
            ws_socket: null,
            message_list: [],
            new_message: null,
            input_message: '',
            channel_choice: '',
        };
        this.choose_channel = this.choose_channel.bind(this);
        this.send_message = this.send_message.bind(this);
        this.change_input_message = this.change_input_message.bind(this);
        this.change_channel_choice = this.change_channel_choice.bind(this);
    }

    change_input_message (event) {
        this.setState({input_message: event.target.value});
    }

    change_channel_choice (event) {
        this.setState({channel_choice: event.target.value});
    }

    start_ws (channel) {
        var url = "ws://" + location.host + "/chatsocket/" + channel;
        var ws_socket = new WebSocket(url)
        ws_socket.onmessage = (event) => {
            this.setState(function(prevState) {
                return {
                    message_list:  [...prevState.message_list, JSON.parse(event.data)]
                };
            });
        };
        this.setState({ws_socket: ws_socket});
    }

    send_message () {
        const text = document.getElementById("message_text").value.trim();
        if (! text || text.length < 1) {
            return
        }
        const new_message = {
            'timestamp': new Date(),
            "author": null,
            "body" : text,
            "id": new Date()
        };
        this.setState({input_message: ''});
        this.state.ws_socket.send(JSON.stringify(new_message));
    }

    choose_channel () {
        const current_channel = document.getElementById("channel_text").value.trim();
        this.setState({
            current_channel: current_channel
        });
        if (current_channel && current_channel.length > 0) {
            this.setState({message_list: []})
            this.start_ws(current_channel);
        }
    }

    render () {
        const navbar_style = {
            top: 0,
            left: 0,
            right: 0,
            zIndex: 255,
            position: 'fixed',
        };
        const margin_inbox_style = {
            paddingTop: '70px',
            paddingBottom: '70px',
        };
        return (
            <div>
                <section className="hero is-primary" style={navbar_style}>
                    <div className="hero-head">
                        <header className="nav">
                            <div className="container">
                                <div className="nav-left">
                                    <a className="nav-item is-active">
                                        <span className="icon">
                                            <i className="fa fa-commenting"></i>
                                        </span>
                                        <span>SimpleTchat</span>
                                    </a>
                                </div>
                                <span id="menu_toggle" className="nav-toggle">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </span>
                                <div id="menu_content" className="nav-right nav-menu">
                                    <span className="nav-item">
                                        <ChannelSelector choose_channel={this.choose_channel} change_channel_choice={this.change_channel_choice} channel_choice={this.state.channel_choice}/>
                                    </span>
                                    <span className="nav-item">
                                        <a className="button is-primary is-inverted" href="/logout">
                                            <span className="icon">
                                                <i className="fa fa-sign-in"></i>
                                            </span>
                                            <span>Sign out</span>
                                        </a>
                                    </span>
                                    <span className="nav-item">
                                        <a className="button is-primary is-inverted" href="https://github.com/toast254/SimpleTchat">
                                            <span className="icon">
                                                <i className="fa fa-github"></i>
                                            </span>
                                            <span>Fork</span>
                                        </a>
                                    </span>
                                </div>
                            </div>
                        </header>
                    </div>
                </section>
                <section className="section is-small" style={margin_inbox_style}>
                    { this.state.current_channel &&
                        <Inbox current_channel={this.state.current_channel} send_message={this.send_message} message_list={this.state.message_list} current_user={this.state.current_user} input_message={this.state.input_message} change_input_message={this.change_input_message} />
                    }
                    { ! this.state.current_channel &&
                        <div className="has-text-centered">
                            <p className="notification is-primary">
                                Choose a channel
                            </p>
                        </div>
                    }
                </section>
            </div>
        )
    }
}

ReactDOM.render(
    <Room />,
    document.getElementById('room_content')
);
