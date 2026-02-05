import Link from "next/link";

export default function HomePage() {
  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>CORE ERP</h1>
        <p style={styles.subtitle}>
          Choose an option to continue
        </p>

        <div style={styles.btnRow}>
          <Link href="/signup" style={{ ...styles.btn, ...styles.signup }}>
            SIGN UP
          </Link>

          <Link href="/login" style={{ ...styles.btn, ...styles.login }}>
            LOGIN
          </Link>
        </div>
      </div>
    </div>
  );
}

const styles: any = {
  page: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #0f172a, #1e293b)",
    padding: "20px",
  },
  card: {
    width: "100%",
    maxWidth: "420px",
    background: "rgba(255,255,255,0.06)",
    border: "1px solid rgba(255,255,255,0.12)",
    borderRadius: "18px",
    padding: "30px",
    textAlign: "center",
    backdropFilter: "blur(10px)",
    boxShadow: "0 20px 60px rgba(0,0,0,0.4)",
  },
  title: {
    color: "white",
    fontSize: "32px",
    fontWeight: 800,
    marginBottom: "8px",
    letterSpacing: "1px",
  },
  subtitle: {
    color: "rgba(255,255,255,0.7)",
    fontSize: "15px",
    marginBottom: "25px",
  },
  btnRow: {
    display: "flex",
    gap: "12px",
    justifyContent: "center",
  },
  btn: {
    flex: 1,
    padding: "12px 14px",
    borderRadius: "12px",
    textDecoration: "none",
    fontWeight: 700,
    fontSize: "14px",
    transition: "0.2s",
    textAlign: "center",
  },
  signup: {
    background: "white",
    color: "#0f172a",
  },
  login: {
    background: "rgba(255,255,255,0.12)",
    color: "white",
    border: "1px solid rgba(255,255,255,0.2)",
  },
};
