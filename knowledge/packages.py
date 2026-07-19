"""Knowledge Packages — Forge's atomic knowledge unit.

The core hypothesis: the graph should return EVIDENCE, not document pointers.
A package is the 5 pieces the model actually needs — canonical import, key
functions, one verified example, one known mistake, relevant project pattern —
plus a confidence/verified flag so unverified knowledge can be filtered out.

ponytail: a plain dict is the store. No YAML dep, no DB. Add a loader only when
packages live in separate files.
"""

PACKAGES = {
    "jwt-go": {
        "concept": "JWT",
        "language": "Go",
        "verified": True,
        "confidence": 100,
        "source": "github.com/golang-jwt/jwt v5 (official, maintained)",
        "imports": ["github.com/golang-jwt/jwt/v5"],
        "functions": [
            "jwt.NewWithClaims(method, claims) *jwt.Token",
            "token.SignedString(key []byte) (string, error)",
            "jwt.ParseWithClaims(tokenStr, claims, keyFunc) (*jwt.Token, error)",
            "jwt.RegisteredClaims{}  // standard claims (exp, sub, iat)",
        ],
        "example": (
            'import "github.com/golang-jwt/jwt/v5"\n\n'
            'claims := jwt.RegisteredClaims{\n'
            '    Subject:   userID,\n'
            '    ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Hour)),\n'
            '}\n'
            'token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)\n'
            'signed, err := token.SignedString([]byte(secret))'
        ),
        "mistakes": [
            "Always trim the 'Bearer ' prefix from the Authorization header before parsing.",
        ],
    },
    "chi-go": {
        "concept": "Chi router",
        "language": "Go",
        "verified": True,
        "confidence": 100,
        "source": "github.com/go-chi/chi v5 (official)",
        "imports": ["github.com/go-chi/chi/v5", "github.com/go-chi/chi/v5/middleware"],
        "functions": [
            "chi.NewRouter() *chi.Mux",
            "r.Use(middleware.Logger)",
            "r.Post(pattern string, http.HandlerFunc)",
            "r.Get(pattern string, http.HandlerFunc)",
        ],
        "example": (
            'import "github.com/go-chi/chi/v5"\n\n'
            'r := chi.NewRouter()\n'
            'r.Post("/login", loginHandler)\n'
            'http.ListenAndServe(":8080", r)'
        ),
        "mistakes": [],
    },
}


def render(*keys):
    """Render evidence packages into prompt text. This is what the model receives
    instead of raw doc pages."""
    out = []
    for k in keys:
        p = PACKAGES.get(k)
        if not p or not p["verified"]:   # skip unverified knowledge
            continue
        out.append(f"### EVIDENCE: {p['concept']} ({p['language']})  [source: {p['source']}]")
        out.append("OFFICIAL IMPORT(S):\n  " + "\n  ".join(p["imports"]))
        out.append("OFFICIAL FUNCTIONS:\n  " + "\n  ".join(p["functions"]))
        out.append("VERIFIED EXAMPLE:\n" + p["example"])
        if p["mistakes"]:
            out.append("KNOWN MISTAKES:\n  - " + "\n  - ".join(p["mistakes"]))
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    print(render("jwt-go", "chi-go"))
