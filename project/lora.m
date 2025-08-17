clc; clear; close all;

%% -------------------- Parameters --------------------
SF = 7;         % Spreading Factor
BW = 125e3;     % Bandwidth
Fs = 1e6;       % Sampling rate
SYMBOL_DURATION = (2^SF)/BW;  % Symbol duration in seconds

%% -------------------- File I/O Setup --------------------
output_filename='output lora.txt'
% Read input bits from file
fid = fopen('alert_bits.txt', 'r');
binary_str = fscanf(fid, '%s');
fclose(fid);

% Convert to numeric array
input_bits = double(binary_str - '0');  % Creates [0,1,0,1,...] array


% Ensure input bits are multiple of SF
if mod(length(input_bits), SF) ~= 0
    % Pad with zeros to make multiple of SF
    padding = zeros(1, SF - mod(length(input_bits), SF));
    input_bits = [input_bits, padding];
    fprintf('Padded with %d zeros to make multiple of SF\n', length(padding));
end

%% -------------------- Processing Setup --------------------
num_symbols = length(input_bits) / SF;
received_bits = zeros(1, length(input_bits));
symbol_errors = 0;
bit_errors = 0;

fprintf('Processing %d symbols (%d bits)...\n', num_symbols, length(input_bits));

%% -------------------- Main Processing Loop --------------------
for sym_idx = 1:num_symbols
    % Convert bits to symbol
    start_bit = (sym_idx-1)*SF + 1;
    end_bit = sym_idx*SF;
    bit_chunk = input_bits(start_bit:end_bit);
    tx_symbol = bi2de(bit_chunk, 'left-msb');
    
    % --- Transmitter ---
    chirp_signal = lora_modulator(tx_symbol, SF, BW, Fs);
    
    % --- Receiver ---
    [rx_symbol, confidence] = lora_receiver(real(chirp_signal), imag(chirp_signal), SF, BW, Fs);
    
    % Convert symbol back to bits
    rx_bit_chunk = zeros(1, SF);
    for i = 1:SF
        rx_bit_chunk(i) = bitget(rx_symbol, i);  % LSB first
    end
    
    % Store received bits
    received_bits(start_bit:end_bit) = rx_bit_chunk;
    
    
    % Error tracking
    if tx_symbol ~= rx_symbol
        symbol_errors = symbol_errors + 1;
        bit_errors = bit_errors + sum(bit_chunk ~= rx_bit_chunk);
    end
    
    % Progress display
    if mod(sym_idx, 100) == 0
        fprintf('Processed %d/%d symbols (%.1f%%)\n', ...
                sym_idx, num_symbols, 100*sym_idx/num_symbols);
    end

    
end

%% -------------------- Results & Output --------------------
% Write received bits to file
% Store received bits as characters ('0' and '1')
received_characters = char('0' + received_bits);

% Write as text file
fileID = fopen(output_filename, 'wt');  % 't' for text mode
fwrite(fileID, received_characters, 'char');
fclose(fileID);
fprintf('Wrote %d characters to output file: %s\n', length(received_characters), output_filename);

% Calculate error rates
symbol_error_rate = symbol_errors / num_symbols;
bit_error_rate = bit_errors / length(input_bits);

fprintf('\n--- Performance Summary ---\n');
fprintf('Symbol Errors: %d/%d (%.4f%%)\n', ...
        symbol_errors, num_symbols, 100*symbol_error_rate);
fprintf('Bit Errors: %d/%d (%.4f%%)\n', ...
        bit_errors, length(input_bits), 100*bit_error_rate);
fprintf('Confidence Metric: %.4f\n', confidence);

%% -------------------- Functions --------------------

% ----------------- LoRa Modulator -----------------
function chirp_signal = lora_modulator(tx_symbol, SF, BW, Fs)
    N = 2^SF;
    SAMPLES_PER_SYMBOL = Fs * N / BW;
    t = (0:SAMPLES_PER_SYMBOL-1)/Fs;
    Tsym = N/BW;

    % Generate base upchirp
    phase = 2*pi * (-BW/2 * t + (BW/(2*Tsym)) * t.^2);
    base_chirp = exp(1i * phase);

    % Apply symbol-dependent phase shift
    phase_shift = 2*pi * tx_symbol/N * (0:SAMPLES_PER_SYMBOL-1);
    chirp_signal = base_chirp .* exp(1i * phase_shift);
end

% ----------------- LoRa Receiver -----------------


function [symbol_out, confidence] = lora_receiver(rx_I, rx_Q, SF, BW, Fs)
    N = 2^SF;
    SAMPLES_PER_SYMBOL = Fs * N / BW;

    if length(rx_I) >= SAMPLES_PER_SYMBOL
        rx_signal = complex(rx_I(1:SAMPLES_PER_SYMBOL), rx_Q(1:SAMPLES_PER_SYMBOL));

        % Generate reference downchirp
        downchirp = lora_modulator(0, SF, BW, Fs);
        downchirp = conj(downchirp);

        % Dechirp received signal
        dechirped = rx_signal .* downchirp;

        % FFT
        fft_out = fft(dechirped, N);

        % Find symbol
        [max_val, idx] = max(abs(fft_out));
        symbol_out = mod(idx-1, N);  % Correct mapping
        confidence = max_val / norm(fft_out, 2);
    else
        symbol_out = 0;
        confidence = 0;
    end
end
