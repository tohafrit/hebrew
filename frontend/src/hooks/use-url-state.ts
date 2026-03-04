import { useSearchParams } from "react-router-dom";
import { useCallback, useMemo } from "react";

/**
 * Sync a single search parameter with URL.
 * Returns [value, setValue] similar to useState.
 */
export function useUrlParam(
  key: string,
  defaultValue = ""
): [string, (val: string) => void] {
  const [searchParams, setSearchParams] = useSearchParams();

  const value = searchParams.get(key) ?? defaultValue;

  const setValue = useCallback(
    (val: string) => {
      setSearchParams(
        (prev) => {
          const next = new URLSearchParams(prev);
          if (val === defaultValue || val === "") {
            next.delete(key);
          } else {
            next.set(key, val);
          }
          return next;
        },
        { replace: true }
      );
    },
    [key, defaultValue, setSearchParams]
  );

  return [value, setValue];
}

/**
 * Sync a numeric search parameter with URL.
 * Returns [value, setValue] where value is number | null.
 */
export function useUrlNumParam(
  key: string
): [number | null, (val: number | null) => void] {
  const [searchParams, setSearchParams] = useSearchParams();

  const raw = searchParams.get(key);
  const value = raw !== null ? Number(raw) : null;

  const setValue = useCallback(
    (val: number | null) => {
      setSearchParams(
        (prev) => {
          const next = new URLSearchParams(prev);
          if (val === null) {
            next.delete(key);
          } else {
            next.set(key, String(val));
          }
          return next;
        },
        { replace: true }
      );
    },
    [key, setSearchParams]
  );

  return [value, setValue];
}

/**
 * Set multiple search params at once (useful when resetting filters).
 */
export function useSetUrlParams() {
  const [, setSearchParams] = useSearchParams();

  return useCallback(
    (updates: Record<string, string | null>) => {
      setSearchParams(
        (prev) => {
          const next = new URLSearchParams(prev);
          for (const [key, val] of Object.entries(updates)) {
            if (val === null || val === "") {
              next.delete(key);
            } else {
              next.set(key, val);
            }
          }
          return next;
        },
        { replace: true }
      );
    },
    [setSearchParams]
  );
}
