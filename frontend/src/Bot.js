import React from 'react'

class Bot extends React.Component {
    render() {
        return(
            <df-messenger
                intent="WELCOME"
                chat-title="fake_news_bot"
                agent-id="935ccdf7-dfff-4c6b-b623-6fe2e950f71b"
                language-code="en"
            ></df-messenger>
        )
    }
}

export default Bot;
