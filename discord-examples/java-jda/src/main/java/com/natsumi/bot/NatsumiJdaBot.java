package com.natsumi.bot;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.interactions.commands.OptionType;

import java.net.URI;
import java.net.http.*;
import java.nio.charset.StandardCharsets;

public class NatsumiJdaBot extends ListenerAdapter {
    private static final ObjectMapper mapper = new ObjectMapper();
    private static final String API_URL = System.getenv().getOrDefault("NATSUMI_API_URL", "http://127.0.0.1:7860").replaceAll("/+$", "");
    private final HttpClient http = HttpClient.newHttpClient();

    public static void main(String[] args) throws Exception {
        String token = System.getenv("DISCORD_TOKEN");
        if (token == null || token.isBlank()) {
            throw new IllegalStateException("DISCORD_TOKEN 환경변수를 넣어줘.");
        }

        JDA jda = JDABuilder.createDefault(token)
                .addEventListeners(new NatsumiJdaBot())
                .build();

        jda.updateCommands().addCommands(
                net.dv8tion.jda.api.interactions.commands.build.Commands.slash("나츠미", "나츠미 AI에게 물어봅니다.")
                        .addOption(OptionType.STRING, "메시지", "예: 서울 한강 온도는 어때", true)
        ).queue();

        System.out.println("Natsumi JDA Bot started.");
    }

    @Override
    public void onSlashCommandInteraction(SlashCommandInteractionEvent event) {
        if (!event.getName().equals("나츠미")) return;

        String message = event.getOption("메시지").getAsString();
        event.deferReply().queue();

        java.util.concurrent.CompletableFuture.supplyAsync(() -> ask(event.getUser().getId(), message))
                .thenAccept(reply -> event.getHook().editOriginal(cut(reply)).queue())
                .exceptionally(err -> {
                    err.printStackTrace();
                    event.getHook().editOriginal("나츠미 AI 서버랑 연결이 안 돼 😿").queue();
                    return null;
                });
    }

    private String ask(String userId, String message) {
        try {
            String body = mapper.writeValueAsString(new AssistantRequest(userId, message));
            HttpRequest req = HttpRequest.newBuilder()
                    .uri(URI.create(API_URL + "/assistant"))
                    .timeout(java.time.Duration.ofSeconds(90))
                    .header("Content-Type", "application/json; charset=utf-8")
                    .POST(HttpRequest.BodyPublishers.ofString(body, StandardCharsets.UTF_8))
                    .build();

            HttpResponse<String> res = http.send(req, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
            if (res.statusCode() < 200 || res.statusCode() >= 300) {
                return "AI 서버 오류야: " + res.statusCode() + " 😿";
            }

            JsonNode json = mapper.readTree(res.body());
            return json.path("reply").asText("답변이 비었어 😾");
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static String cut(String s) {
        if (s == null) return "답변이 비었어 😾";
        return s.length() > 2000 ? s.substring(0, 1990) + "..." : s;
    }

    public record AssistantRequest(String user_id, String message) {}
}
