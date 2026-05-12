import axios from "axios";
import { SlashCommandBuilder } from "discord.js";

const NATSUMI_API_URL = process.env.NATSUMI_API_URL || "http://127.0.0.1:7860";

export default {
  data: new SlashCommandBuilder()
    .setName("나츠미")
    .setDescription("나츠미 AI에게 물어봅니다.")
    .addStringOption(option =>
      option.setName("메시지")
        .setDescription("예: 서울 한강 온도는 어때")
        .setRequired(true)
    ),

  async execute(interaction) {
    await interaction.deferReply();
    const message = interaction.options.getString("메시지");

    try {
      const res = await axios.post(`${NATSUMI_API_URL}/assistant`, {
        user_id: interaction.user.id,
        message,
      }, { timeout: 90000 });

      await interaction.editReply((res.data.reply || "답변이 비었어 😾").slice(0, 2000));
    } catch (err) {
      console.error(err);
      await interaction.editReply("나츠미 AI 서버랑 연결이 안 돼 😿");
    }
  },
};
