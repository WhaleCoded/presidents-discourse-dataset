use clap::{self, clap_app};
use std::collections::HashMap;
use std::env;
use std::fs;
use std::io::Write;
use std::path;

#[tokio::main]
async fn main() {
    let matches = clap::clap_app!(downloader_cli =>
        (about: "Starts an instance of the embedder service")
        (version: "1.0")
        (@arg PATH: -p --path +takes_value "The path to where the data should be stored")
        (@arg NUM_WORKERS: -n --num_workers +takes_value "The number of workers to use")
    )
    .get_matches();

    let storage_path = match matches.value_of("PATH") {
        Some(user_path) => path::Path::new(user_path).to_path_buf(),
        None => env::current_dir().unwrap().join("data").join("html"),
    };

    let num_workers = match matches.value_of("NUM_WORKERS") {
        Some(num) => num.parse::<usize>().unwrap(),
        None => 50,
    };

    let json_str = fs::read_to_string(
        env::current_dir()
            .unwrap()
            .join("data")
            .join("document_urls.json"),
    )
    .unwrap();
    let download_urls: HashMap<String, (String, Option<String>)> =
        serde_json::from_str(&json_str).unwrap();

    let download_run_time = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(num_workers)
        .build()
        .unwrap();

    for (url, (primary, sub)) in &download_urls {
        let url_clone = url.clone();
        let primary_clone = primary.clone();
        let sub_clone = sub.clone();
        let storage_path = storage_path.clone();
        download_run_time.spawn(async move {
            let response = reqwest::get(url_clone.clone())
                .await
                .unwrap()
                .text()
                .await
                .unwrap();
            let file_destination = match sub_clone {
                Some(sub_string) => storage_path
                    .join(primary_clone)
                    .join(sub_string)
                    .join(url_clone),
                None => storage_path.join(primary_clone).join(url_clone),
            };
            let mut file = fs::File::create(file_destination).unwrap();
            file.write_all(response.as_bytes()).unwrap();
        });
    }
}
