//PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
//Released under the MIT License <http://opensource.org/licenses/MIT>

package pyj2d;

import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.SourceDataLine;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.ShortBuffer;


public class Mixer {

    AudioFormat audioFormat;
    int buffer;
    int sampleByte;
    int sampleMax;
    int sampleMin;
    ByteOrder endian;
    int[] shift;
    double[] data;
    int dataLen;
    SourceDataLine line;

    /**
     * Mixer combines multiple audio data input to a single output. Can operate
     * with javax.sound.sampled, input obtained from an AudioInputStream and
     * output directed to a SourceDataLine. Supports PCM 16-bit audio format.
     * Argument audioFormat and buffer are the AudioFormat and buffer size to 
     * initialize the mixer and the SourceDataLine.
     */
    public Mixer(AudioFormat audioFormat, int buffer) {
        this.audioFormat = audioFormat;
        this.buffer = buffer;
        this.sampleByte = audioFormat.getSampleSizeInBits() == 16 ? 2 : 1;
        this.sampleMax = audioFormat.getSampleSizeInBits() == 16 ? 32767 : 127;
        this.sampleMin = audioFormat.getSampleSizeInBits() == 16 ? -32768 : -128;
        this.endian = !audioFormat.isBigEndian() ? ByteOrder.LITTLE_ENDIAN : ByteOrder.BIG_ENDIAN;
        this.shift = !audioFormat.isBigEndian() ? new int[] {0,8} : new int[] {8,0};
        this.line = getLine(this.audioFormat, this.buffer);
        if (this.line == null)
            this.line = getLine(this.audioFormat, this.buffer, true);
        if (this.line != null)
            this.buffer = this.line.getBufferSize();
            this.data = new double[this.buffer/this.sampleByte];
            this.dataLen = 0;
        }

    /**
    Obtain line from default system mixer.
    Argument audioFormat and buffer is the AudioFormat and write buffer of the line.
    */
    private SourceDataLine getLine(AudioFormat audioFormat, int buffer) {
        javax.sound.sampled.Mixer mixer;
        DataLine.Info lineFormat = new DataLine.Info(SourceDataLine.class, audioFormat);
        try {
            mixer = AudioSystem.getMixer(null);
            }
        catch (IllegalArgumentException e) { return null; }
        catch (SecurityException e) { return null; }
        try {
            this.line = (SourceDataLine) mixer.getLine(lineFormat);
            this.line.open(audioFormat, buffer);
            this.line.start();
            }
        catch (LineUnavailableException e) { return null; }
        catch (IllegalArgumentException e) { return null; }
        catch (SecurityException e) { return null; }
        return this.line;
        }

    /**
    Obtain line available from system mixers.
    Argument audioFormat and buffer is the AudioFormat and write buffer of the line.
    */
    private SourceDataLine getLine(AudioFormat audioFormat, int buffer, boolean scan) {
        if (!scan)
            return getLine(audioFormat, buffer);
        javax.sound.sampled.Mixer mixer;
        javax.sound.sampled.Mixer.Info[] mixerInfo = AudioSystem.getMixerInfo();
        DataLine.Info lineFormat = new DataLine.Info(SourceDataLine.class, audioFormat);
        for (int i=0; i<mixerInfo.length; i++) {
            try {
                mixer = AudioSystem.getMixer(mixerInfo[i]);
                if (!mixer.isLineSupported(lineFormat))
                    continue;
                }
            catch (IllegalArgumentException e) { continue; }
            catch (SecurityException e) { continue; }
            try {
                this.line = (SourceDataLine) mixer.getLine(lineFormat);
                this.line.open(audioFormat, buffer);
                this.line.start();
                return this.line;
                }
            catch (LineUnavailableException e) { continue; }
            catch (IllegalArgumentException e) { continue; }
            catch (SecurityException e) { continue; }
            }
        return null;
        }

    /**
    Get mixer line.
    */
    public SourceDataLine getLine() {
        return this.line;
        }

    /**
    Set mixer line. Line should support AudioFormat initialized.
    */
    public void setLine(SourceDataLine line) {
        if (this.line != null)
            close();
        this.line = line;
        try {
            if (!this.line.isOpen())
                this.line.open(this.audioFormat, this.buffer);
            this.buffer = this.line.getBufferSize();
            this.data = new double[this.buffer/this.sampleByte];
            this.dataLen = 0;
            this.line.start();
            }
        catch (LineUnavailableException e) { this.line=null; }
        catch (IllegalArgumentException e) { this.line=null; }
        catch (SecurityException e) { this.line=null; }
        }

    /**
    Close mixer line.
    */
    public void close() {
        if (this.line != null)
            try {
                this.line.stop();
                this.line.flush();
                this.line.close();
                }
            catch (SecurityException e) {}
        this.line = null;
        }

    /**
    Start mixer line.
    */
    public void start() {
        if (this.line != null)
            this.line.start();
        }

    /**
    Stop mixer line.
    */
    public void stop() {
        if (this.line != null)
            this.line.stop();
        }

    /**
    Uninitialize mixer.
    */
    public void quit() {
        close();
        this.data = null;    
        }    

    /**
    Check if mixer line is initialized.
    */
    public boolean isInitialized() {
        return (this.line != null);
        }

    /**
    * Add audio data to the mixer buffer.
    * Argument data is the audio data in a ByteArray, dataLen is the
    * length of data to use, lvolume and rvolume is for L/R volume adjustment
    * of values 0.0 to 1.0.
    */
    public void setAudioData(byte[] data, int dataLen, float lvolume, float rvolume) {
        if (!(lvolume < 1.0) && !(rvolume < 1.0))
            setByteData(data, dataLen);
        else
            setByteData(data, dataLen, lvolume, rvolume);
        if (dataLen > this.dataLen)
            this.dataLen = dataLen;
        }

    /**
    * Add audio data to the mixer buffer.
    * Argument data is the audio data in a ByteArray, dataLen is the
    * length of data to use, volume is for volume adjustment of values
    * 0.0 to 1.0.
    */
    public void setAudioData(byte[] data, int dataLen, float volume) {
        setAudioData(data, dataLen, volume, volume);
        }

    /**
    * Add audio data to the mixer buffer.
    * Argument data is the audio data in a ByteArray, dataLen is the
    * length of data to use.
    */
    public void setAudioData(byte[] data, int dataLen) {
        setByteData(data, dataLen);
        }

    /**
    * Add data to internal array.
    */
    private void setByteData(byte[] data, int dataLen) {
        ShortBuffer dataBuffer = ByteBuffer.wrap(data).order(this.endian).asShortBuffer();
        for (int i = 0; i < dataLen/this.sampleByte; i++) {
            this.data[i] += (double) dataBuffer.get(i);
            }
        }

    /**
    * Add data to internal array.
    */
    private void setByteData(byte[] data, int dataLen, float lvolume, float rvolume) {
        ShortBuffer dataBuffer = ByteBuffer.wrap(data).order(this.endian).asShortBuffer();
        for (int i = 0; i < dataLen/this.sampleByte; i+=2) {
            this.data[i] += (double) (dataBuffer.get(i) * lvolume);
            this.data[i+1] += (double) (dataBuffer.get(i+1) * rvolume);
            }
        }

    /**
    * Get mixed audio data.
    * Argument byteArray is a ByteArray the data will be place in.
    * Return data length of ByteArray used.
    */
    public int getAudioData(byte[] byteArray) {
        double samplePeak = checkAudioLevel(this.data, this.dataLen);
        if (samplePeak > this.sampleMax)
            correctAudioLevel(this.data, this.dataLen, samplePeak);
        getByteData(this.data, this.dataLen, byteArray);
        int dataLen = this.dataLen;
        resetMixer();
        return dataLen;
        }

    /**
    * Get mixed data from internal array.
    */
    private void getByteData(double[] data, int dataLen, byte[] byteArray) {
        int pos = 0;
        for (int i = 0; i < dataLen/this.sampleByte; i++) {
            byteArray[pos] = (byte) ((int) (data[i])>>this.shift[0] & 0xff);
            byteArray[pos+1] = (byte) ((int) (data[i])>>this.shift[1] & 0xff);
            pos += this.sampleByte;
            }
        }

    /**
    * Check whether audio data level goes over threshold.
    */
    private double checkAudioLevel(double[] data, int dataLen) {
        double xmax = (double) this.sampleMax;
        double xmin = (double) this.sampleMin;
        for (int i = 0; i < dataLen/this.sampleByte; i++) {
            if (data[i] > xmax)
                xmax = data[i];
            else if (data[i] < xmin)
                xmin = data[i];
            }
        if (Math.abs(xmin)-1 > xmax)
            xmax = (double) Math.abs(xmin)-1;
        return xmax;
        }

    /**
    * Correct audio data level if exceed threshold.
    */
    private void correctAudioLevel(double[] data, int dataLen, double overflow) {
        float correction = (float) (this.sampleMax/overflow);
        for (int i = 0; i < dataLen/this.sampleByte; i++) {
            data[i] = (double) data[i] * correction;
            }
        }

    /**
    * Internal array is zeroed.
    */
    private void resetMixer() {
        for (int i = 0; i < this.dataLen/this.sampleByte; i++) {
            this.data[i] = 0;
            }
        this.dataLen = 0;
        }

    /**
    * Adjust volume of audio data.
    * Argument data is the audio data in a ByteArray, dataLen is the length
    * of data to use, lvolume and rvolume is for L/R volume adjustment
    * of values 0.0 to 1.0.
    * Return input ByteArray adjusted for volume.
    */
    public byte[] processVolume(byte[] data, int dataLen, float lvolume, float rvolume) {
        ShortBuffer dataBuffer = ByteBuffer.wrap(data).order(this.endian).asShortBuffer();
        for (int i = 0; i < dataLen/this.sampleByte; i+=2) {
            dataBuffer.put(i, (short) (dataBuffer.get(i)*lvolume));
            dataBuffer.put(i+1, (short) (dataBuffer.get(i+1)*rvolume));
            }
        return data;
        }

    /**
    * Adjust volume of audio data.
    * Argument data is the audio data in a ByteArray, dataLen is the length
    * of data to use, volume is for volume adjustment of values 0.0 to 1.0.
    * Return input ByteArray adjusted for volume.
    */
    public byte[] processVolume(byte[] data, int dataLen, float volume) {
        byte[] byteArray = processVolume(data, dataLen, volume, volume);
        return byteArray;
        }

    /**
    * Adjust volume of audio data.
    * Argument data is the audio data in a ByteArray, dataLen is the length
    * of data to use.
    * Return input ByteArray adjusted for volume.
    */
    public byte[] processVolume(byte[] data, int dataLen) {
        float volume = (float) 1.0;
        byte[] byteArray = processVolume(data, dataLen, volume, volume);
        return byteArray;
        }

    /**
    * Write audio data to mixer line.
    * Argument data is audio data, offset and length is array data to write.
    * Throw LineUnavailableException exception if mixer line not available.
    */
    public void write(byte[] data, int offset, int length) throws LineUnavailableException {
        try {
            this.line.write(data, offset, length);
            }
        catch (NullPointerException e) {
            throw new LineUnavailableException();
            }
        }

    /**
    * Return mixer data buffer size.
    */
    public int getBufferSize() {
        return this.buffer;
        }

    /**
    * Return AudioFormat of the mixer.
    */
    public AudioFormat getAudioFormat() {
        return this.audioFormat;
        }
    }

