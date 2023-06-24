class Player extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            currentTrack: null
        }

        window.onSpotifyWebPlaybackSDKReady = () => {
              // You can now initialize Spotify.Player and use the SDK

            this.player = new Spotify.Player({
                name: 'HB Project',
                getOAuthToken: callback => {
                    // Run code to get a fresh access token
                    callback(this.props.accessToken);
                    },
                volume: 0.5
            });

            this.player.addListener('not_ready', ({ device_id }) => {
                console.log('Device ID is not ready for playback', device_id);
            });

            this.player.connect().then(success => {
                if (success) {
                console.log('The Web Playback SDK successfully connected to Spotify!');
                }
            });

            this.player.on('ready', async data => {
                let { device_id } = data;
                console.log("Let the music play on!");
            });

            this.player.addListener('player_state_changed', currentTrack => {
                this.setState({currentTrack: currentTrack});
                console.log(currentTrack)
            });
        };
    }
 
    play  = ({
          spotify_uri,
          playerInstance: {
            _options: {
              getOAuthToken,
              id
            }
          }
        }) => {
            fetch(`https://api.spotify.com/v1/me/player/play?device_id=${id}`, {
                method: 'PUT',
                body: JSON.stringify({ uris: [spotify_uri] }),
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.props.accessToken}`
                },
            });
        }

    togglePlay = () => {
        this.player.togglePlay();
    }

    goToNextSong = () => {
        this.props.nextSong();
    }

    goToPreviousSong = () => {
        this.props.previousSong();
    }

    componentDidUpdate(prevProps) {
    // Typical usage (don't forget to compare props):
        if (this.props.songToPlay !== prevProps.songToPlay) {
            this.play ({
                playerInstance: this.player,
                spotify_uri: this.props.songToPlay
            });
        }
    } 
 
    render() {

        let trackName = "";
            if (this.state.currentTrack) {
                trackName = this.state.currentTrack.track_window.current_track.name;
            }

        let artistName = "";
            if (this.state.currentTrack) {
                // artistName = this.state.currentTrack.track_window.current_track.artists[0].name
                artistName = this.state.currentTrack.track_window.current_track.artists.map(artist => artist.name).join(", ")
            }

        let albumArt = "../static/images/turntable.jpeg";
            if (this.state.currentTrack) {
                albumArt = this.state.currentTrack.track_window.current_track.album.images[0].url;
            }

        return (<div>
            <img className="album" src={albumArt} height="400" width="460"></img>

            <p></p>

            <button id="button_bw" className="btn" onClick={this.goToPreviousSong}>
                    <i className="fa fa-backward"></i></button>

            <button id="button_play" className="btn" onClick={this.togglePlay}>
                    <i className="fa fa-play"></i></button>

            <button id="button_fw" className="btn" onClick={this.goToNextSong}>
                    <i className="fa fa-forward"></i></button>

            <p className="track"> Track: {trackName} </p>
            <p className="artists"> Artist(s): {artistName} </p>
            </div>
        );
    }
}