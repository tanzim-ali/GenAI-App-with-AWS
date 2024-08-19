import React, { useEffect, useState } from "react";

const BotMessage = ({ fetchMessage }) => {
  const [message, setMessage] = useState("...");

  useEffect(() => {
    const fetchBotMessage = async () => {
      const response = await fetchMessage();
      setMessage(response);
    };
    fetchBotMessage();
  }, [fetchMessage]);

  return (
    <div className="bot-message">
      <div className="message">{message}</div>
    </div>
  );
};

export default BotMessage;
