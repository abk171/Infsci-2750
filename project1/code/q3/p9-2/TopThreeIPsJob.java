import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;
import java.util.TreeMap;

public class TopThreeIPsJob {
    public static class TopThreeIPsMapper extends Mapper<Object, Text, Text, LongWritable> {
        private Text ip = new Text();
        private LongWritable dataSize = new LongWritable();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String[] parts = value.toString().split("\\s+");
            if (parts.length >= 2) {
                ip.set(parts[0]);
                try {
                    long size = Long.parseLong(parts[1]);
                    dataSize.set(size);
                    context.write(ip, dataSize);
                } catch (NumberFormatException e) {
                    context.getCounter("Mapper Errors", "Number Format Exceptions").increment(1);
                }
            }
        }
        
    }

    public static class TopThreeIPsReducer extends Reducer<Text, LongWritable, Text, LongWritable> {
        private TreeMap<Long, String> topIPsMap = new TreeMap<>();

        public void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException {
            long sum = 0;
            for (LongWritable val : values) {
                sum += val.get();
            }

            // Insert sum and IP into TreeMap
            topIPsMap.put(sum, key.toString());

            // Keep only top 3
            if (topIPsMap.size() > 3) {
                topIPsMap.remove(topIPsMap.firstKey());
            }
        }

        @Override
        protected void cleanup(Context context) throws IOException, InterruptedException {
            // Output the top 3 IPs and their data size
            for (Long size : topIPsMap.descendingKeySet()) {
                context.write(new Text(topIPsMap.get(size)), new LongWritable(size));
            }
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: TopThreeIPsJob <input path> <output path>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Top Three IPs");
        job.setJarByClass(TopThreeIPsJob.class);
        job.setMapperClass(TopThreeIPsMapper.class);
        job.setReducerClass(TopThreeIPsReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(LongWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
