import { Component, type ErrorInfo, type ReactNode } from "react";
import { Button } from "@/components/ui/button";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("ErrorBoundary caught:", error, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4 p-8 text-center">
          <h2 className="text-xl font-bold">Что-то пошло не так</h2>
          <p className="text-muted-foreground max-w-md">
            Произошла непредвиденная ошибка. Попробуйте перезагрузить страницу.
          </p>
          {this.state.error && (
            <pre className="text-xs text-destructive bg-destructive/10 rounded p-3 max-w-lg overflow-auto">
              {this.state.error.message}
            </pre>
          )}
          <Button onClick={() => window.location.reload()}>
            Перезагрузить
          </Button>
        </div>
      );
    }
    return this.props.children;
  }
}
