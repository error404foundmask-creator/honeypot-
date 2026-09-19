use chrono::{DateTime, Utc};
use reqwest::Client;
use serde::Serialize;
use std::{env, net::SocketAddr, sync::Arc};
use tokio::{io::AsyncReadExt, net::{TcpListener, TcpStream}, time::{timeout, Duration}};
use tracing::{error, info};
use uuid::Uuid;

#[derive(Serialize, Clone)]
struct Event { event_id: Uuid, timestamp: DateTime<Utc>, source_ip: String, source_port: u16, destination_port: u16, protocol: String, service: String, event_type: String, demo: bool }

async fn handle(mut socket: TcpStream, addr: SocketAddr, port: u16, protocol: &'static str, service: &'static str, client: Arc<Client>, ingest: String) {
    let event = Event { event_id: Uuid::new_v4(), timestamp: Utc::now(), source_ip: addr.ip().to_string(), source_port: addr.port(), destination_port: port, protocol: protocol.into(), service: service.into(), event_type: "connection_attempt".into(), demo: false };
    let _ = client.post(&ingest).json(&event).send().await;
    let mut buf = [0u8; 1024];
    let _ = timeout(Duration::from_secs(5), socket.read(&mut buf)).await;
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();
    let ingest = env::var("EVENT_INGEST_URL").unwrap_or_else(|_| "http://127.0.0.1:8000/api/events".into());
    let client = Arc::new(Client::builder().timeout(Duration::from_secs(3)).build()?);
    let services = [(2222, "SSH", "ssh_decoy"), (8080, "HTTP", "http_decoy"), (2121, "FTP", "ftp_decoy"), (5433, "DB", "db_decoy")];
    for (port, protocol, service) in services { let listener = TcpListener::bind(("0.0.0.0", port)).await?; let c = client.clone(); let url = ingest.clone(); tokio::spawn(async move { info!(port, service, "decoy listening"); loop { match listener.accept().await { Ok((socket, addr)) => { let c2=c.clone(); let u=url.clone(); tokio::spawn(handle(socket, addr, port, protocol, service, c2, u)); }, Err(e) => error!(%e, "accept failed") } } }); }
    tokio::signal::ctrl_c().await?; Ok(())
}
