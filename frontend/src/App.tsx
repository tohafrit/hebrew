import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "@/components/theme-provider";
import { NikkudProvider } from "@/components/nikkud-provider";
import { RootLayout } from "@/components/layout/root-layout";
import { ProtectedRoute } from "@/components/layout/protected-route";
import { HomePage } from "@/pages/home";
import { LoginPage } from "@/pages/login";
import { RegisterPage } from "@/pages/register";
import { DictionaryPage } from "@/pages/dictionary";
import { SRSPage } from "@/pages/srs";
import { AlphabetPage } from "@/pages/alphabet";
import { GrammarPage } from "@/pages/grammar";
import { LessonsPage } from "@/pages/lessons";
import { ReadingPage } from "@/pages/reading";
import { ListeningPage } from "@/pages/listening";
import { WritingPage } from "@/pages/writing";
import { DialoguesPage } from "@/pages/dialogues";
import { DashboardPage } from "@/pages/dashboard";
import { AchievementsPage } from "@/pages/achievements";
import { CulturePage } from "@/pages/culture";
import { SettingsPage } from "@/pages/settings";
import { TopicsPage } from "@/pages/topics";
import { ReaderPage } from "@/pages/reader";
import { PathPage } from "@/pages/path";
import { ConjugationDrillPage } from "@/pages/conjugation-drill";
import { MistakesPage } from "@/pages/mistakes";
import { PronunciationPage } from "@/pages/pronunciation";
import { PlacementPage } from "@/pages/placement";
import { HandwritingPage } from "@/pages/handwriting";
import { MinimalPairsPage } from "@/pages/minimal-pairs";
import { ClozePage } from "@/pages/cloze";
import { LeaderboardPage } from "@/pages/leaderboard";
import { RootExplorerPage } from "@/pages/root-explorer";
import { GrammarCardsPage } from "@/pages/grammar-cards";
import { NotFoundPage } from "@/pages/not-found";
import { ErrorBoundary } from "@/components/error-boundary";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, refetchOnWindowFocus: false },
  },
});

export default function App() {
  return (
    <ErrorBoundary>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <NikkudProvider>
        <BrowserRouter>
          <Routes>
            <Route element={<RootLayout />}>
              <Route element={<ProtectedRoute />}>
                <Route path="/" element={<HomePage />} />
                <Route path="/dictionary" element={<DictionaryPage />} />
                <Route path="/srs" element={<SRSPage />} />
                <Route path="/alphabet" element={<AlphabetPage />} />
                <Route path="/grammar" element={<GrammarPage />} />
                <Route path="/conjugation-drill" element={<ConjugationDrillPage />} />
                <Route path="/mistakes" element={<MistakesPage />} />
                <Route path="/lessons" element={<LessonsPage />} />
                <Route path="/lessons/:lessonId" element={<LessonsPage />} />
                <Route path="/reading" element={<ReadingPage />} />
                <Route path="/reading/:textId" element={<ReadingPage />} />
                <Route path="/listening" element={<ListeningPage />} />
                <Route path="/writing" element={<WritingPage />} />
                <Route path="/dialogues" element={<DialoguesPage />} />
                <Route path="/dialogues/:dialogueId" element={<DialoguesPage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/achievements" element={<AchievementsPage />} />
                <Route path="/culture" element={<CulturePage />} />
                <Route path="/settings" element={<SettingsPage />} />
                <Route path="/topics" element={<TopicsPage />} />
                <Route path="/reader" element={<ReaderPage />} />
                <Route path="/path" element={<PathPage />} />
                <Route path="/pronunciation" element={<PronunciationPage />} />
                <Route path="/handwriting" element={<HandwritingPage />} />
                <Route path="/minimal-pairs" element={<MinimalPairsPage />} />
                <Route path="/cloze" element={<ClozePage />} />
                <Route path="/cloze/:textId" element={<ClozePage />} />
                <Route path="/leaderboard" element={<LeaderboardPage />} />
                <Route path="/root-explorer" element={<RootExplorerPage />} />
                <Route path="/grammar-cards" element={<GrammarCardsPage />} />
              </Route>
              <Route path="/placement" element={<PlacementPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="*" element={<NotFoundPage />} />
            </Route>
          </Routes>
        </BrowserRouter>
        </NikkudProvider>
      </ThemeProvider>
    </QueryClientProvider>
    </ErrorBoundary>
  );
}
